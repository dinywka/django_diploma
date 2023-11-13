import React from "react";
import { Link } from "react-router-dom";

export function Navbar1() {
  return (
      <header className="d-flex justify-content-center py-3">
        <ul className="nav nav-pills">
          <li className="nav-item"><Link to={"/"} className="nav-link px-2 text-secondary">
                Домашняя
              </Link></li>
          <li className="nav-item"><Link to={"/about"} className="nav-link px-2 text-secondary">
                О нас
              </Link></li>
          <li className="nav-item"><Link to={"/pricing"} className="nav-link px-2 text-secondary">
                Цены
              </Link></li>
          <li className="nav-item"><Link to={"/register"} className="nav-link px-2 text-secondary">
                Зарегестрироваться
              </Link></li>
        </ul>
      </header>
  );
}