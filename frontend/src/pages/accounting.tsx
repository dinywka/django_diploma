import { Link } from "react-router-dom";
import React from "react";
import * as bases from "../components/ui/base";
import _default from "react-redux/es/components/connect";

export default function Page() {
  return (
    <bases.Base1>
      <div className="p-5 mb-4 bg-light rounded-3">
        <div className="container-fluid py-5">
          <h1 className="display-5 fw-bold">Новостной портал</h1>
          <p className="col-md-8 fs-4">Using a series of utilities, you can create this jumbotron, just like the one in
            previous versions of Bootstrap. Check out the examples below for how you can remix and restyle it to your
            liking.</p>
          <button className="btn btn-primary btn-lg" type="button">Добавить новость</button>
        </div>
      </div>
    </bases.Base1>
  );
}