import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Basic from "./components/Basic";
import Login from "./Login/Login";
import Register from "./Register/Register";
import Update from "./Update/Update";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" Component={Login} />
        <Route path="/register" Component={Register} />
        <Route path="/update" Component={Update} />
        <Route path="/new-user" Component={Basic} />
      </Routes>
    </Router>
  );
}

export default App;
