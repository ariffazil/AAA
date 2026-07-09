import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ExplorePage from "./pages/ExplorePage";
import WealthPage from "./pages/WealthPage";
import WellPage from "./pages/WellPage";
import StatusPage from "./pages/StatusPage";
import ForgePage from "./pages/ForgePage";
import KernelPage from "./pages/KernelPage";
import InitPage from "./pages/InitPage";
import SealPage from "./pages/SealPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/explore" replace />} />
        <Route path="/explore" element={<ExplorePage />} />
        <Route path="/wealth" element={<WealthPage />} />
        <Route path="/well" element={<WellPage />} />
        <Route path="/status" element={<StatusPage />} />
        <Route path="/forge" element={<ForgePage />} />
        <Route path="/kernel" element={<KernelPage />} />
        <Route path="/init" element={<InitPage />} />
        <Route path="/seal" element={<SealPage />} />
      </Routes>
    </BrowserRouter>
  );
}
