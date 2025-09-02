import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./EmailPage.css"; // Certifique-se de criar este arquivo CSS

function EmailPage() {
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const handleContinue = () => {
    if (email) {
      
      // Lógica de autenticação ou navegação
      navigate("/");
    } else {
      alert("Por favor, digite seu e-mail.");
    }
  };

  return (
    <div className="email-page-container">
      <div className="email-form-card">
        <h2 className="form-title">Informe o seu e-mail para continuar</h2>
        <input
          type="email"
          placeholder="Informe o seu e-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="email-input"
        />
        <p className="privacy-text">
          O Lombra Delivery poderá enviar comunicações neste e-mail. Caso não queira receber
          comunicações neste canal, não será possível utilizar o App
        </p>
        <button className="continue-btn" onClick={handleContinue}>
          Continuar
        </button>
      </div>
    </div>
  );
}

export default EmailPage;