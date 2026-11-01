import { BrowserRouter, Routes, Route } from 'react-router-dom'

import MainLayout from './layouts/MainLayout'

import Board from './pages/Board/Board'
import Chats from './pages/Chats/Chats'
import Notes from './pages/Notes/Notes'
import Tasks from './pages/Tasks/Tasks'

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<MainLayout />}>
                    <Route path="/" element={<Board />} />
                    <Route path="/chats" element={<Chats />} />
                    <Route path="/notes" element={<Notes />} />
                    <Route path="/tasks" element={<Tasks />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App