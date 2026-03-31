from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Patient, Donor, Recipient
from medical_records.models import MedicalRecord
from .serializers import PatientSerializer, DonorSerializer, RecipientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.hospital:
            return Patient.objects.filter(hospital=self.request.user.hospital)
        return Patient.objects.all()

    def perform_create(self, serializer):
        serializer.save(hospital=self.request.user.hospital)

class DonorViewSet(viewsets.ModelViewSet):
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.hospital:
            return Donor.objects.filter(donor_id__hospital=self.request.user.hospital)
        return Donor.objects.all()

class RecipientViewSet(viewsets.ModelViewSet):
    serializer_class = RecipientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.hospital:
            return Recipient.objects.filter(recipient_id__hospital=self.request.user.hospital)
        return Recipient.objects.all()


# --- Unified View ---

class UnifiedPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns a flattened list of patients for the TC Table.
        Combines Patient, Donor/Recipient, and MedicalRecord info.
        """
        hospital = request.user.hospital
        if not hospital:
            return Response({"error": "User not associated with a hospital"}, status=403)

        patients = Patient.objects.filter(hospital=hospital).prefetch_related('donor_profile', 'recipient_profile')
        
        data = []
        for p in patients:
            # Determine if Donor or Recipient
            p_type = "Donor" if hasattr(p, 'donor_profile') else "Recipient"
            
            # Get Medical State (Only for Donors)
            med_state = "N/A"
            if p_type == "Donor":
                med_state = getattr(p.donor_profile, 'medical_state', 'Living')

            data.append({
                "patient_id": p.patient_id,
                "name": p.name, # Ensure you added this field to Patient model
                "patient_type": p_type,
                "organ": p.organ_type,
                "blood_type": p.blood_type,
                "medical_state": med_state,
                "urgency": p.urgency_level,
                "created_at": p.created_at
            })
        
        return Response(data)

    def post(self, request):
        """
        Processes the unified registration form.
        Creates: Patient -> Profile (Donor/Rec) -> MedicalRecord.
        """
        data = request.data
        hospital = request.user.hospital
        serializer = UnifiedPatientSerializer(data=request.data)

        if serializer.is_valid():
            clean_data = serializer.validated_data
            try:
                with transaction.atomic():
                    # Now use clean_data.get('name') instead of request.data.get('name')
                    # ... the rest of your creation logic ...
                    return Response({"status": "success"}, status=201)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        return Response(serializer.errors, status=400)

        if not hospital:
            return Response({"error": "Authorized Hospital required"}, status=400)

        try:
            with transaction.atomic():
                # 1. Create Patient
                patient = Patient.objects.create(
                    name=data.get('name'),
                    hospital=hospital,
                    blood_type=data.get('blood_type'), # e.g. "A+"
                    organ_type=data.get('organ'),
                    medical_history=f"Initial registration for {data.get('organ')}",
                    urgency_level=5 
                )

                # 2. Create Donor or Recipient profile
                p_type = data.get('patient_type')
                if p_type == 'Donor':
                    Donor.objects.create(
                        donor_id=patient,
                        medical_state=data.get('medical_state', 'LIVING').upper(),
                        consent_status=True
                    )
                else:
                    Recipient.objects.create(
                        recipient_id=patient,
                        waiting_list_status='ACTIVE'
                    )

                # 3. Create General Medical Record
                # We store height, weight, BP in the JSON lab_results field
                MedicalRecord.objects.create(
                    patient=patient,
                    record_type='GENERAL',
                    test_date=data.get('lab_date'),
                    lab_results={
                        "weight": data.get('weight'),
                        "height": data.get('height'),
                        "blood_pressure": data.get('blood_pressure')
                    },
                    verified_status=False
                )

                return Response({"message": "Patient registered successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)