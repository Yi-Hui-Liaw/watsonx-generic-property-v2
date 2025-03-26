import React from "react";
import PropertyCard from "../components/PropertyCard";
import "../styles/HomePage.css";

const properties = [
  { id: 1, title: "The Nexus One", location: "Kuala Lumpur", image: "/assets/nexus-one.jpg", link: "/nexus-one" },
  { id: 2, title: "The Lumenh", location: "Penang", image: "/assets/lumenh.jpg", link: "/lumenh" },
  { id: 3, title: "ABC Residence", location: "Langkawi", image: "/assets/abc-residence.jpg", link: "/abc-residence" }
];

const HomePage = () => {
  return (
    <div className="homepage">
      <div className="hero">
        <h1>Find Your Dream Property with AI</h1>
        <p>Describe what you're looking for, and let AI recommend the best properties.</p>
        <input type="text" placeholder="E.g. Luxury condo in Kuala Lumpur" />
        <button>🔍 Search with AI</button>
      </div>

      <h2>Or Explore These Properties</h2>
      <div className="property-grid">
        {properties.map((property) => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>
    </div>
  );
};

export default HomePage;
