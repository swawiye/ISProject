import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function LogIn() {
    return (
    <div>
      <div className="flex items-center justify-center min-h-screen bg-[#042d6d]">
        <form
          // onSubmit={handleSubmit}
          className="w-full max-w-md bg-white p-8 rounded-xl shadow-lg space-y-6"
        >
          <h2 className="text-2xl font-bold text-center text-[#042d6d]">
            Welcome Back !
          </h2>

          {/* {error && <p className="text-red-500 text-center">{}</p>} */}
          <div>
            <label className="block mb-1">Email address</label>
            <input
              type="email"
              name="email"
              // value={form.email}
              // onChange={handleChange}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#042d6d]"
              placeholder="Enter your email"
            />
          </div>

          <div>
            <label className="block mb-1">Password</label>
            <input
              type="password"
              name="password"
              // value={form.password}
              // onChange={handleChange}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#042d6d]"
              placeholder="Enter your password"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-[#042d6d] text-white font-semibold py-2 rounded-lg hover:bg-[#3871a0] transition"
          >
            Log In
          </button>
        </form>
      </div>
    </div>
    )
}

export default LogIn;