
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
    TYPE: string;
    ID: number;
    POSITION: number[];
    SPEED: number;
    DIRECTION: number;
    MAXSPEED: number;
    CURHEALTH: number;
    MAXHEALTH: number;
    CURENERGY: number; // On Ships, Only Yours
    MAXENERGY: number;
    ENERGYRECHARGERATE: number;
    MASS: number;
    HITRADIUS: number;
    TIMEALIVE: number;
    INBODY: boolean;
}

interface IShipData extends IObjectData {
    RADARRANGE: number;
    ROTATION: number;
    ROTATIONSPEED: number;
    CURSHIELD: number;
    MAXSHIELD: number;
    CMDQ: string[]; // Only Your Ship
}

interface IEnvironment {
    GAMEDATA: IGameData;
    MESSAGES: string[];
    RADARDATA: IObjectData[];
    RADARLEVEL: number;
    SHIPDATA: IShipData;
}

interface IRequest {
    WORLDWIDTH: number;
    WORLDHEIGHT: number;
    GAMENAME: string;
    IMAGELENGTH: number;
}
