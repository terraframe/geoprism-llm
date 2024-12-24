import ActionProvider from "./ActionProvider";

// MessageParser starter code
class MessageParser {
    actionProvider: ActionProvider;
    state: any;

    constructor(actionProvider: ActionProvider, state: any) {
        this.actionProvider = actionProvider;
        this.state = state;
    }

    parse(message: string) {
        this.actionProvider.invokeBedrock(message);
    }
}

export default MessageParser;