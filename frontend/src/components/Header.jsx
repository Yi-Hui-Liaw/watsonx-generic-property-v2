import React from "react";
import "../styles/Header.css";
import logo from "../assets/SH-Logo.png";
import searchIcon from "../assets/search.png";

const Header = () => {
  return (
    <header className="header">
      <div className="logo-container">
        <img src={logo} alt="Logo" className="logo-image" />
        <div className="logo">Sweet Home</div>
        <div className="titles">
          <div className="title">About Us</div>
          <div className="title">Contact</div>
          <div className="title">Blog</div>
        </div>
      </div>
      <nav className="login-signup-container">
        <div className="login-signup">
          <img src={searchIcon} alt="Search" className="search-icon" />
          <div className="login">Log In</div>
        </div>
        <div className="divider"></div> {/* Vertical Divider */}
        <div className="sign-up">Sign Up</div>
      </nav>
    </header>
  );
};

export default Header;
