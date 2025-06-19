import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import HomePage from "./pages/HomePage";
import NexusOne from "./pages/NexusOne";
import Lumenh from "./pages/Lumenh";
import ABCResidence from "./pages/ABCResidence";

function App() {
  useEffect(() => {
    window.watsonAssistantChatOptions = {
      integrationID: "e4b87da5-1d16-4c8f-98bc-c1c2c0d74bb5",
      region: "us-south",
      serviceInstanceID: "8647c42c-c307-4270-91ad-ed481a325879",
      onLoad: async (instance) => {
        await instance.render();

        const style = document.createElement('style');
        style.innerHTML = `
          .WACWidget {
            width: 35% !important;
            height: 85% !important;
          }
          .WatsonAssistantChatHost {
            margin: 0px;
          }
        `;
        document.head.appendChild(style);
      },
    };

    const script = document.createElement("script");
    script.src = `https://web-chat.global.assistant.watson.appdomain.cloud/versions/${
      window.watsonAssistantChatOptions.clientVersion || "latest"
    }/WatsonAssistantChatEntry.js`;
    script.async = true;
    document.head.appendChild(script);
  }, []);

  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/nexus-one" element={<NexusOne />} />
        <Route path="/lumenh" element={<Lumenh />} />
        <Route path="/abc-residence" element={<ABCResidence />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
