// Bracket.js
import React, { useEffect, useState } from "react";
import axios from "axios";

function Bracket({ competitionId }) {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    axios.get(`/get_bracket/${competitionId}`).then((response) => {
      setMatches(response.data);
    });
  }, [competitionId]);

  return (
    <div>
      <h1>Competition Bracket</h1>
      <div className="bracket">
        {matches.map((match) => (
          <div key={match.id} className="match">
            <p>
              {match.participant1 || "TBD"} vs {match.participant2 || "TBD"}
            </p>
            <p>Date: {match.date || "TBD"}</p>
            <p>Result: {match.result || "Pending"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Bracket;
