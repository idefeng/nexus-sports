import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Stats } from './pages/Stats';
import { Explorer } from './pages/Explorer';
import { Import } from './pages/Import';
import { ActivityDetail } from './pages/ActivityDetail';
import { SettingsPage } from './pages/Settings';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="/explorer" element={<Explorer />} />
          <Route path="/import" element={<Import />} />
          <Route path="/activity/:id" element={<ActivityDetail />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
