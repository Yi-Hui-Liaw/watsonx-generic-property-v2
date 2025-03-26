import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import HomePage from "./pages/HomePage";
import NexusOne from "./pages/NexusOne";
import Lumenh from "./pages/Lumenh";
import ABCResidence from "./pages/ABCResidence";

function App() {
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
