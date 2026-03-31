from rest_framework import serializers
from .models import Patient, Donor, Recipient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        # Ensure 'name' is in your model fields if you added it!
        fields = ['patient_id', 'name', 'hospital', 'blood_type', 'organ_type', 'medical_history', 'urgency_level', 'created_at']
        read_only_fields = ['hospital'] 

class DonorSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source='donor_id'
    )
    
    class Meta:
        model = Donor
        # Added 'medical_state' to match our logic
        fields = ['patient_id', 'consent_status', 'availability', 'medical_state']

class RecipientSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source='recipient_id'
    )
    
    class Meta:
        model = Recipient
        fields = ['patient_id', 'waiting_list_status']


# --- The Unified "Bridge" Serializer ---

class UnifiedPatientSerializer(serializers.Serializer):
    """
    This serializer handles the incoming JSON from the TCPatients.jsx form.
    It doesn't map to a single model; it validates the entire 'bundle'.
    """
    # Patient Fields
    name = serializers.CharField(max_length=255)
    patient_type = serializers.ChoiceField(choices=['Donor', 'Recipient'])
    organ = serializers.CharField(max_length=100) # Maps to organ_type in model
    blood_type = serializers.CharField(max_length=10)
    
    # Donor Specific (Optional if Recipient)
    medical_state = serializers.ChoiceField(choices=['LIVING', 'DECEASED', 'Living', 'Deceased'], required=False)
    
    # Medical Record Fields (Store in JSONField in DB)
    lab_date = serializers.DateField()
    weight = serializers.FloatField()
    height = serializers.FloatField()
    blood_pressure = serializers.CharField(max_length=20)

    def validate(self, data):
        """Custom validation: Ensure Donors have a medical state."""
        if data.get('patient_type') == 'Donor' and not data.get('medical_state'):
            raise serializers.ValidationError({"medical_state": "This field is required for donors."})
        return data