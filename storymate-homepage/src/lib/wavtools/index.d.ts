export class WavRecorder {
    begin(): Promise<void>;
    record(callback: (data: { mono: Int16Array }) => void): Promise<void>;
    stop(): Promise<void>;
}

export class WavStreamPlayer {
    interrupt(): Promise<{ trackId?: string }>;
} 