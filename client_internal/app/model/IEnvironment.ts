
interface IGameData {
    BESTSCORE: number;
    DEATHS: number;
    HIGHSCORE: number;
    LSTDSTRBY: string;
    ROUNDTIME: number;
    SCORE: number;
    TIMELEFT: number;
}

interface IObjectData {
    MASS: number;
    ID: number;
    POSITION: number[];
    SPEED: number;
    TIMEALIVE: number;
    HITRADIUS: number;
    TYPE: string;
}

interface IShipData extends IObjectData {
    CMDQ: string[];
}

interface IEnvironment {
    GAMEDATA: IGameData;
    MESSAGES: string[];
    RADARDATA: IObjectData[];
    RADARLEVEL: number;
    SHIPDATA: IShipData;
}