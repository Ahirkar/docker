import { Button } from "@mui/material";
import { Link } from "react-router-dom";
import React from "react";
import "./Login.css";

const Login = () => {
  return (
    <div className="container">
      <Link to="/register">
        <Button variant="contained">Register</Button>
      </Link>
      <Link to="/new-user">
        <Button variant="contained">New User</Button>
      </Link>
      <Link to="/update">
        <Button variant="contained">Update</Button>
      </Link>
    </div>
  );
};

export default Login;
