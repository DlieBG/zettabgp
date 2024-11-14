export interface MRTLibrary {
    scenarios: MRTScenario[];
}

export interface MRTScenario {
    id: string;
    path: string;
    name: string;
    description: string;
    no_rabbitmq_direct: boolean;
    rabbitmq_grouped: boolean;
    no_mongodb_log: boolean;
    no_mongodb_state: boolean;
    no_mongodb_statistics: boolean;
    clear_mongodb: boolean;
    playback_speed: number;
    mrt_files: string[];
}

export interface MRTScenarioRequest {
    id: string;
}

export interface MRTScenarioResponse {
    count_announce: number;
    count_withdraw: number;
}
