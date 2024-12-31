import React from "react";

const Bracket = ({ rounds }) => {
  return (
    <div className="bracket">
      {rounds.map((round, index) => (
        <div key={index} className="round">
          {round.map((match, i) => (
            <div key={i} className="match">
              <div>{match.team1 || "TBD"}</div>
              <div>vs</div>
              <div>{match.team2 || "TBD"}</div>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default Bracket;
