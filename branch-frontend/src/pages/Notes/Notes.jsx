import { useState, useEffect } from "react"
import "./Notes.css"

function Notes() {
    const [notes, setNotes] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5173/api/notes/all?user_id=1111-112").then(res => res.json()).then(data => setNotes(data));
    }, []);       
    
    
    return (
        <section>
            <h1>Мои заметки</h1>

            <div className="notes">
                {notes.map(note => (
                    <div className="note" key={note.id}>
                        <h3>{note.header}</h3>
                        <p>{note.text}</p>
                    </div>
                ))}
            </div>
        </section>
    )
}

export default Notes;