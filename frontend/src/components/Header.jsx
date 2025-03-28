import React from "react";
import { Link } from "react-router-dom";
import "../styles/Header.css";
import logo from "../assets/SH-Logo.png";
import searchIcon from "../assets/search.png";

const Header = () => {
  return (
    <header className="header">
      <div className="logo-container">
        <Link to="/" className="logo-link">
          <img src={logo} alt="Logo" className="logo-image" />
          <div className="logo">Sweet Home</div>
        </Link>
        <div className="titles">
          <div className="title-t">About Us</div>
          <div className="title-t">Contact</div>
          <div className="title-t">Blog</div>
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
