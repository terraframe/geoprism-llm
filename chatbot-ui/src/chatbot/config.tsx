
import { v4 as uuidv4 } from 'uuid';

const config = {
    initialMessages: [],
    botName: "Geospatial Finder",
    customStyles: {
        botMessageBox: {
            backgroundColor: "#376B7E",
        },
        chatButton: {
            backgroundColor: "#376B7E",
        },
    },
    state: { sessionId: uuidv4() },
}

export default config