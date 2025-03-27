import React from "react";
import "../styles/Footer.css";

import fbIcon from "../assets/facebook.png";  
import igIcon from "../assets/instagram.png"; 
import twIcon from "../assets/twitter.png";  

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-column">
          <h4>About Us</h4>
          <p>We provide the best property solutions for your needs.</p>
        </div>
        <div className="footer-column">
          <h4>Contact</h4>
          <p>Email: info@sweethome.com</p>
          <p>Phone: +60 123 456 789</p>
        </div>
      </div>
      <div className="footer-bottom">
        <div className="footer-icons">
          <a href="#" className="footer-icon">
            <img src={fbIcon} alt="Facebook" className="social-icon" />
          </a>
          <a href="#" className="footer-icon">
            <img src={igIcon} alt="Instagram" className="social-icon" />
          </a>
          <a href="#" className="footer-icon">
            <img src={twIcon} alt="Twitter" className="social-icon" />
          </a>
        </div>
        <div className="footer-links">
          <a href="#">Privacy Policy</a>
          <a href="#">Terms of Service</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
