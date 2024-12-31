import React from "react";
import Bracket from "./components/Bracket";

function App() {
  return (
    <div>
      <h1>Tournament Management App</h1>
      {/* Replace competitionId with the actual ID */}
      <Bracket competitionId={1} />
    </div>
  );
}

export default App;
