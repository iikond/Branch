import { NavLink } from 'react-router-dom'
import './Sidebar.css'

function Sidebar() {
    return (
        <div className='container'>
            <aside>
                <h2>Branch</h2>

                <nav>
                    <NavLink to="/">Доска</NavLink>
                    <NavLink to="/chats">Чаты</NavLink>
                    <NavLink to="/notes">Заметки</NavLink>
                    <NavLink to="/tasks">Задачи</NavLink>
                </nav>
            </aside>
        </div>
    )
}

export default Sidebar