import React from "react";
import {
    BedrockAgentRuntimeClient,
    InvokeAgentCommand,
} from "@aws-sdk/client-bedrock-agent-runtime";
import Loader from "./Loader";
import instance from "../SessionHolder";


/**
 * Invokes a Bedrock agent to run an inference using the input
 * provided in the request body.
 *
 * @param {string} prompt - The prompt that you want the Agent to complete.
 * @param {string} sessionId - An arbitrary identifier for the session.
 */
export const invokeBedrockAgent = async (prompt: string, sessionId: string) => {

    const region = process.env.REACT_APP_AGENT_REGION as string;
    const accessKeyId = process.env.REACT_APP_ACCESS_KEY_ID as string;
    const secretAccessKey = process.env.REACT_APP_SECRET_ACCESS_KEY as string;

    const client = new BedrockAgentRuntimeClient({
        region: region,
        credentials: {
            accessKeyId: accessKeyId,
            secretAccessKey: secretAccessKey
        }
    });

    const agentId = process.env.REACT_APP_AGENT_ID;
    const agentAliasId = process.env.REACT_APP_AGENT_ALIAS_ID;

    const command = new InvokeAgentCommand({
        agentId,
        agentAliasId,
        sessionId,
        inputText: prompt,
    });

    try {
        let completion = "";
        const response = await client.send(command);

        if (response.completion === undefined) {
            throw new Error("Completion is undefined");
        }

        for await (const chunkEvent of response.completion) {
            const chunk = chunkEvent.chunk;

            if (chunk != undefined) {
                console.log(chunk);
                const decodedResponse = new TextDecoder("utf-8").decode(chunk.bytes);
                completion += decodedResponse;
            }
        }

        return { sessionId: sessionId, completion };
    } catch (err) {
        console.error(err);
    }
};

/**
 * Invokes a Bedrock agent to run an inference using the input
 * provided in the request body.
 *
 * @param {string} prompt - The prompt that you want the Agent to complete.
 * @param {string} sessionId - An arbitrary identifier for the session.
 */
export const invokeApiAgent = async (prompt: string, sessionId: string) => {

    try {
        const params = new URLSearchParams({ prompt, sessionId });

        const response = await fetch(process.env.REACT_APP_API_URL + '?' + params);
        const data = await response.json();

        return { sessionId: data.sessionId, completion: data.content };
    } catch (err) {
        console.error(err);
    }
};


class ActionProvider {

    createChatBotMessage: any;
    setState: any;
    createClientMessage: any;
    stateRef: any;
    createCustomMessage: any;

    constructor(
        createChatBotMessage: any,
        setState: any,
        createClientMessage: any,
        stateRef: any,
        createCustomMessage: any,
    ) {
        this.createChatBotMessage = createChatBotMessage;
        this.setState = setState;
        this.createClientMessage = createClientMessage;
        this.stateRef = stateRef;
        this.createCustomMessage = createCustomMessage;
    }


    async invokeBedrock(message: string) {
        const loading = this.createChatBotMessage(<Loader />)
        this.setState((prev: any) => ({ ...prev, messages: [...prev.messages, loading], }))

        // const result = await invokeBedrockAgent(message, this.sessionId);
        const result = await invokeApiAgent(message, instance.getSessionId());

        const responseMessage = this.createChatBotMessage(result?.completion)

        this.setState((prev: any) => {
            // Remove Loading here
            const newPrevMsg = prev.messages.slice(0, -1)
            return { ...prev, messages: [...newPrevMsg, responseMessage], }
        })

    }
}

export default ActionProvider;