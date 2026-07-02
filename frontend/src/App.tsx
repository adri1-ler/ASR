import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Dashboard from "./pages/Dashboard";
import SectionPage from "./pages/SectionPage";
import Channel from "./pages/Channel";
import Notification from "./pages/Notification";
import Player from "./pages/Player";
import Reaction from "./pages/Reaction";
import Sport from "./pages/Sport";
import Standing from "./pages/Standing";
import Team from "./pages/Team";
import User from "./pages/User";
import Matchstatistics from "./pages/Matchstatistics";
import Favoriteplayer from "./pages/Favoriteplayer";
import Tournamentround from "./pages/Tournamentround";
import Channelmember from "./pages/Channelmember";
import Bracketslot from "./pages/Bracketslot";
import Mediafile from "./pages/Mediafile";
import Stadium from "./pages/Stadium";
import Lineup from "./pages/Lineup";
import Lineupplayer from "./pages/Lineupplayer";
import Prematchodds from "./pages/Prematchodds";
import Matchpreview from "./pages/Matchpreview";
import Tennisset from "./pages/Tennisset";
import Competition from "./pages/Competition";
import Favoritecompetition from "./pages/Favoritecompetition";
import Favoriteteam from "./pages/Favoriteteam";
import Friendship from "./pages/Friendship";
import Match from "./pages/Match";
import Matchevent from "./pages/Matchevent";
import Message from "./pages/Message";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/overview/:sectionId" element={<SectionPage />} />
            <Route path="/channel" element={<Channel />} />
            <Route path="/notification" element={<Notification />} />
            <Route path="/player" element={<Player />} />
            <Route path="/reaction" element={<Reaction />} />
            <Route path="/sport" element={<Sport />} />
            <Route path="/standing" element={<Standing />} />
            <Route path="/team" element={<Team />} />
            <Route path="/user" element={<User />} />
            <Route path="/matchstatistics" element={<Matchstatistics />} />
            <Route path="/favoriteplayer" element={<Favoriteplayer />} />
            <Route path="/tournamentround" element={<Tournamentround />} />
            <Route path="/channelmember" element={<Channelmember />} />
            <Route path="/bracketslot" element={<Bracketslot />} />
            <Route path="/mediafile" element={<Mediafile />} />
            <Route path="/stadium" element={<Stadium />} />
            <Route path="/lineup" element={<Lineup />} />
            <Route path="/lineupplayer" element={<Lineupplayer />} />
            <Route path="/prematchodds" element={<Prematchodds />} />
            <Route path="/matchpreview" element={<Matchpreview />} />
            <Route path="/tennisset" element={<Tennisset />} />
            <Route path="/competition" element={<Competition />} />
            <Route path="/favoritecompetition" element={<Favoritecompetition />} />
            <Route path="/favoriteteam" element={<Favoriteteam />} />
            <Route path="/friendship" element={<Friendship />} />
            <Route path="/match" element={<Match />} />
            <Route path="/matchevent" element={<Matchevent />} />
            <Route path="/message" element={<Message />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
