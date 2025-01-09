"use client"

import { useRouter } from "next/navigation";
import { useState } from "react";

const LoginPage = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const router = useRouter();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const body = new URLSearchParams({
        grant_type: "password",
        username: formData.username, // Replace with user input
        password: formData.password, // Replace with user input
        scope: "",
        client_id: "string",
        client_secret: "string",
      });
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body.toString(), // URL-encoded string
      });
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("token", data.access_token);
        router.push("/dashboard");
      } else {
        alert("Invalid credentials");
      }
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  )
}

export default LoginPage