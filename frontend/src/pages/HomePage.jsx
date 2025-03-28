import React from "react";
import PropertyCard from "../components/PropertyCard";
import "../styles/HomePage.css";
import searchIcon from "../assets/search.png";
import nexusOne from "../assets/nexus-1.png";
import lumenh from "../assets/lumenh-1.png";
import abc from "../assets/abc-1.png";

const properties = [
    { 
      id: 1, 
      title: "The Nexus One", 
      location: "Kuala Lumpur", 
      image: nexusOne, 
      link: "/nexus-one", 
      additionalInfo: "Revolutionary freehold Development. <br /><br />Prices from <strong>$300,000 </strong>" 
    },
    { 
      id: 2, 
      title: "The Lumenh", 
      location: "Mutiara Damansara", 
      image: lumenh, 
      link: "/lumenh", 
      additionalInfo: "Pioneering residence in the COLLECTIVE edition. <br /><br />Prices from <strong>$500,000 </strong>" 
    },
    { 
      id: 3, 
      title: "ABC Residence", 
      location: "Damansara Bay", 
      image: abc, 
      link: "/abc-residence", 
      additionalInfo: "Bold and distinct approach to luxury living. <br /><br />Prices from <strong>$800,000 </strong>" 
    }
  ];
  

const HomePage = () => {
  return (
    <div className="homepage">
      <div className="hero">
        <h1>Discover your next Home with us</h1>
        <p>Describe what you're looking for, and let us recommend the best properties.</p>
        
        {/* Search bar with icon */}
        <div className="search-bar">
          <input type="text" placeholder="E.g. Luxury condo in the Valley" />
          <img src={searchIcon} alt="Search" className="search-icon-i" />
        </div>
      </div>

      <div className="explore-title">
        <h2>Or Explore These Properties</h2>
      </div>  

      <div className="property-grid">
        {properties.map((property) => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>

      <div className="quote">
        <h2>
            <span className="white-text">A future home ... </span> 
            <span className="black-text">with Endless Possibilities.</span>
        </h2>
      </div>
    </div>
  );
};

export default HomePage;
