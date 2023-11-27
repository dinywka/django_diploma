// Page.tsx
import React, { useState, useEffect } from "react";
import * as bases from "../components/ui/base";

interface User {
  id: number;
  username: string;
}

const Page: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);

  const fetchData = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/");
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []); // Run once when the component mounts

  return (
    <bases.Base1>
      <div className="p-5 mb-4 bg-light rounded-3">
        <div className="container-fluid py-5">
          <h1 className="display-5 fw-bold">Корпоративный портал</h1>
          <p className="col-md-8 fs-4">
            Добро пожаловать на корпоративный портал нашей компании! Для
            продолжения работы, пожалуйста, войдите в аккаунт!
          </p>
          <button
            className="btn btn-primary btn-lg"
            type="button"
            onClick={fetchData}
          >
            Получить инфо
          </button>

          {/* Display the fetched user data */}
          <ul>
            {users.map((user) => (
              <li key={user.id}>{user.username}</li>
            ))}
          </ul>
        </div>
      </div>
    </bases.Base1>
  );
};

export default Page;
