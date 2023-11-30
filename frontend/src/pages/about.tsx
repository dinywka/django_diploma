import React, { useState } from "react";

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

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h1 style={titleStyle}>Корпоративный портал</h1>
        <p style={subtitleStyle}>
          Для получения списка пользователей нажмите на кнопку
        </p>
        <button style={buttonStyle} type="button" onClick={fetchData}>
          Получить инфо
        </button>
      </div>
      <ul style={listStyle}>
        {users.map((user) => (
          <li key={user.id} style={listItemStyle}>
            {user.username}
          </li>
        ))}
      </ul>
    </div>
  );
};

const containerStyle = {
  padding: "5rem",
  marginBottom: "4rem",
  background: "#f8f9fa",
  borderRadius: "0.3rem",
};

const headerStyle = {
  marginBottom: "2rem",
};

const titleStyle = {
  fontSize: "2.5rem",
  fontWeight: "bold",
};

const subtitleStyle = {
  fontSize: "1.25rem",
  color: "#6c757d",
};

const buttonStyle = {
  fontSize: "1.5rem",
  padding: "0.75rem 1.5rem",
  background: "#007bff",
  color: "#fff",
  border: "none",
  borderRadius: "0.25rem",
  cursor: "pointer",
  transition: "background 0.3s",
};

const listStyle = {
  listStyle: "none",
  padding: 0,
};

const listItemStyle = {
  fontSize: "1.25rem",
  marginBottom: "0.5rem",
};

export default Page;
