
# Next.js Frontend for FastAPI Starter Template

This is a Next.js project designed to work with the FastAPI starter template backend. It provides a responsive and modern frontend for user authentication and other API integrations.

---

## Features

- **Next.js Framework**: Server-side rendering (SSR), static site generation (SSG), and client-side rendering (CSR) supported.
- **User Authentication**: Integrates with the FastAPI backend for JWT-based authentication.
- **Responsive Design**: Built with modern UI libraries like Tailwind CSS (optional) for mobile and desktop compatibility.
- **Environment Variable Management**: Configure API endpoints and keys securely with `.env.local`.

---

## Prerequisites

Ensure you have the following installed:

- **Node.js**: Version 14.x or later
- **npm** or **yarn**
- **FastAPI Backend**: Running on `http://127.0.0.1:8000` or your configured URL.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/codenameberyl/nextjs-fastapi-mongodb.git
cd nextjs-fastapi-mongodb/frontend
```

### 2. Install Dependencies

```bash
# With npm
npm install

# Or with yarn
yarn install
```

### 3. Configure Environment Variables

Create a `.env.local` file in the project root and add the following variables:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api/v1
```

- Replace the `NEXT_PUBLIC_API_URL` with your FastAPI backend URL.

### 4. Run the Development Server

```bash
# With npm
npm run dev

# Or with yarn
yarn dev
```

Open your browser and navigate to `http://localhost:3000`.

---

## Project Structure

```plaintext
.
├── app/                     # App Router directory
│   ├── layout.tsx            # Main layout for the application
│   ├── page.tsx              # Home page
│   ├── auth/                # Authentication pages
│   │   ├── login/           # Login page
│   │   │   ├── page.tsx      # Login component
│   │   │   └── styles.css   # Login-specific styles (optional)
│   │   ├── register/        # Register page
│   │   │   ├── page.tsx      # Register component
│   │   │   └── styles.css   # Register-specific styles (optional)
│   ├── dashboard/           # Protected routes
│   │   ├── page.tsx          # Dashboard main page
│   ├── globals.css          # Global styles
├── components/              # Reusable components
├── public/                  # Static assets
├── utils/                   # Helper functions (e.g., API requests, auth handling)
├── .env.local               # Environment variables
├── next.config.ts           # Next.js configuration
├── package.json             # Project metadata and dependencies
```

---

## Authentication Workflow

This frontend is designed to work seamlessly with the FastAPI backend for JWT-based authentication.

1. **Login**:
   - The user submits their credentials via the login form.
   - The credentials are sent to the `/login` endpoint of the FastAPI backend.
   - On success, a JWT token is returned and stored in `localStorage` or `cookies`.

2. **Protected Routes**:
   - Use a custom `AuthGuard` component or middleware to protect routes.
   - Verify the token's validity before rendering protected pages.

3. **Logout**:
   - Clear the stored token and redirect the user to the login page.

---

## Scripts

### Development

```bash
npm run dev
```

### Build for Production

```bash
npm run build
```

### Start Production Server

```bash
npm run start
```

---

## Example Components

#### `app/layout.js` (Main Layout)

This file defines the layout for your entire application.

```jsx
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="container mx-auto">
          <header>
            <h1 className="text-2xl font-bold">FastAPI + Next.js</h1>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
```

---

#### `app/page.js` (Home Page)

This is the default landing page.

```jsx
export default function HomePage() {
  return (
    <div>
      <h1>Welcome to the Next.js Frontend</h1>
      <p>This is the main landing page of the application.</p>
    </div>
  );
}
```

---

#### `app/auth/login/page.js` (Login Page)

A login page that integrates with your FastAPI backend.

```jsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const router = useRouter();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
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
  );
}
```

---

#### `app/dashboard/page.js` (Protected Dashboard)

A protected page that requires authentication.

```jsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth/login");
      return;
    }

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/protected-route`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((err) => {
        console.error(err);
        router.push("/auth/login");
      });
  }, [router]);

  return (
    <div>
      <h1>Dashboard</h1>
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>Loading...</p>}
    </div>
  );
}
```

---

## Dependencies

### Core Libraries

- **Next.js**: React framework for SSR and SSG.
- **React**: For building user interfaces.
- **Tailwind CSS** (Optional): Utility-first CSS framework for styling.

### Authentication

- **JWT Decode** (Optional): For decoding and verifying JWT tokens.

### API Calls

- **Axios** (Optional): Promise-based HTTP client.

---

## Deployment

### Vercel (Recommended)
1. Push your code to GitHub or another Git provider.
2. Go to [Vercel](https://vercel.com/) and import your repository.
3. Set the environment variables in the Vercel dashboard.
4. Deploy your application.

### Other Hosting Options
- **Netlify**
- **AWS Amplify**
- **Custom VPS**

---

## License

This project is licensed under the [MIT License](/LICENSE).

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## Contact

For questions or support, reach out to:

- **Email**: abiolaonasanya22@example.com
- **GitHub**: [codenameberyl](https://github.com/codenameberyl)

