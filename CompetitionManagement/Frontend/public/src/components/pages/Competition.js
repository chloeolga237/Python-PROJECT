import React, { useState, useEffect } from "react";
import { createCompetition, generateBracket } from "../api";
import Bracket from "../components/Bracket";

const Competition = () => {
  const [name, setName] = useState("");
  const [bracket, setBracket] = useState([]);

  const handleCreate = async () => {
    const response = await createCompetition({ name, user_id: 1 }); // Replace 1 with dynamic user ID
    console.log(response.data);
  };

  const handleGenerate = async () => {
    const response = await generateBracket(1); // Replace 1 with competition ID
    setBracket(response.data.bracket);
  };

  return (
    <div>
      <h1>Create Competition</h1>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Competition Name"
      />
      <button onClick={handleCreate}>Create</button>

      <h2>Bracket</h2>
      <button onClick={handleGenerate}>Generate Bracket</button>
      <Bracket rounds={bracket} />
    </div>
  );
};

export default Competition;
