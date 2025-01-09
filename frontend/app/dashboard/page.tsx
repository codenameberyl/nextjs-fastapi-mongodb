"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const DashboardPage = () => {
  const [data, setData] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth/login");
      return;
    }

    // fetch(`${process.env.NEXT_PUBLIC_API_URL}/protected-route`, {
    //   headers: { Authorization: `Bearer ${token}` },
    // })
    //   .then((res) => res.json())
    //   .then((data) => setData(data))
    //   .catch((err) => {
    //     console.error(err);
    //     router.push("/auth/login");
    //   });
  }, [router]);

  return (
    <div>
      <h1>Dashboard</h1>
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>Loading...</p>}
    </div>
  )
}

export default DashboardPage