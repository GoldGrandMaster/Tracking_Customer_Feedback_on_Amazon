import React, { useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [search, setSearch] = useState("");
  const [backendResponse, setBackendResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    try {
      setLoading(true);

      const response = await axios.post("http://localhost:5000/asin", {
        ASIN: search,
      });

      // Handle the response from the backend here
      console.log(response.data);

      // Update state to store the backend response
      setBackendResponse(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <h1>Tracking Customer Feedback on Amazon</h1>
      <input type="text" value={search} onChange={(e) => setSearch(e.target.value)} />
      <button onClick={handleSearch}>Run</button>

      {loading && <div>Loading...</div>}

      {backendResponse && (
        <div>
          <h2>Product Information:</h2>
          <div>
            <img src={backendResponse.image_url} alt="Product" style={{ maxWidth: '200px' }} />
          </div>
          <p><strong>Title:</strong> {backendResponse.product_title}</p>
          <p><strong>Price:</strong> {backendResponse.product_price}</p>
          <p><strong>Description:</strong> {backendResponse.product_description}</p>

          <h2>Analysis Result:</h2>
          <p>{backendResponse.analysis_result}</p>

          <h2>Reviews:</h2>
          <ul>
            {backendResponse.reviews.map((review, index) => (
              <li key={index}>
                <p><strong>Name:</strong> {review['name of reviewer']}</p>
                <p><strong>Stars:</strong> {review['number of stars']}</p>
                <p><strong>Date:</strong> {review['date of review']}</p>
                <p><strong>Content:</strong> {review['content of review']}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
};

export default Dashboard;
