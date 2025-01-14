import { v4 as uuidv4 } from 'uuid';

class Singleton {
    sessionId: string;

    constructor() {
        this.sessionId = uuidv4();
    }

    setSessionId(sessionId: string) {
        this.sessionId = sessionId;
    }

    getSessionId() {
        return this.sessionId;
    }
}

const instance = new Singleton();
Object.freeze(instance);

export default instance;