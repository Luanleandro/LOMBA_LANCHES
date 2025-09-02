// import { useState } from "react";
// import "./App.css";

// function App() {
//   const [email, setEmail] = useState("");
//   const [phone, setPhone] = useState("");

//   const handleLogin = (type: string) => {
//     alert(`Login com ${type} ainda não implementado.`);
//   };

//   return (
//     <div className="login-container">
//       {/* Lado esquerdo */}
//       <div className="login-left">
//         <img
//           src="https://static.ifood-static.com.br/image/upload/f_auto/webapp/logo/ifood-logo-2021.png"
//           alt="iFood"
//           className="logo"
//         />
//         <img
//           src="https://illustrations.popsy.co/white/responsibility.svg"
//           alt="Ilustração"
//           className="illustration"
//         />
//       </div>

//       {/* Lado direito */}
//       <div className="login-right">
//         <h1>Falta pouco para matar sua fome!</h1>
//         <p>Como deseja continuar?</p>

//         <button className="btn facebook" onClick={() => handleLogin("Facebook")}>
//           Continuar com Facebook
//         </button>

//         <button className="btn google" onClick={() => handleLogin("Google")}>
//           <img
//             src="https://www.svgrepo.com/show/355037/google.svg"
//             alt="Google"
//             className="icon"
//           />
//           Fazer Login com o Google
//         </button>

//         <div className="btn-row">
//           <button className="btn outline" onClick={() => handleLogin("Celular")}>
//             Celular
//           </button>
//           <button className="btn outline" onClick={() => handleLogin("E-mail")}>
//             E-mail
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;

import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import { useState } from "react";
import EmailPage from "./pages/EmailPage";
import "./App.css";

function Login() {
  const navigate = useNavigate();

  const handleLogin = (type: string) => {
    if (type === "E-mail") {
      navigate("/register/email"); // navega para a página de email
    } else {
      alert(`Login com ${type} ainda não implementado.`);
    }
  };

  return (
    <div className="login-container">
      <div className="login-left">
        {/* <img
          src="https://static.ifood-static.com.br/image/upload/f_auto/webapp/logo/ifood-logo-2021.png"
          alt="iFood"
          className="logo"
        /> */}
        {/* <img
          src="https://illustrations.popsy.co/white/responsibility.svg"
          alt="Ilustração"
          className="illustration"
        /> */}
      </div>

      <div className="login-right">
        <h1>Falta pouco para matar sua fome!</h1>
        <p>Como deseja continuar?</p>

        <button className="btn facebook" onClick={() => handleLogin("Facebook")}>
          Continuar com Facebook
        </button>

        <button className="btn google" onClick={() => handleLogin("Google")}>
          <img
            src="https://www.svgrepo.com/show/355037/google.svg"
            alt="Google"
            className="icon"
          />
          Fazer Login com o Google
        </button>

        <div className="btn-row">
          <button className="btn outline" onClick={() => handleLogin("Celular")}>
            Celular
          </button>
          <button className="btn outline" onClick={() => handleLogin("E-mail")}>
            E-mail
          </button>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register/email" element={<EmailPage />} />
      </Routes>
    </Router>
  );
}

export default App;
