export interface MessageReplayRequest {
    no_rabbitmq_direct: boolean;
    rabbitmq_grouped: number | null;
    no_mongodb_log: boolean;
    no_mongodb_state: boolean;
    no_mongodb_statistics: boolean;
    clear_mongodb: boolean;
    playback_speed: number | null;
    start_time: string;
    end_time: string;
}

export interface MessageReplayResponse {
    count_announce: number;
    count_withdraw: number;
}
