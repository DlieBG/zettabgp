import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { MessageReplayRequest, MessageReplayResponse } from '../../../types/message-replay.type';
import { MessageReplayService } from '../../../services/message-replay/message-replay.service';

@Component({
  selector: 'app-message-replay',
  templateUrl: './message-replay.component.html',
  styleUrl: './message-replay.component.scss'
})
export class MessageReplayComponent {
  message_replay_request: MessageReplayRequest = {
    no_rabbitmq_direct: false,
    rabbitmq_grouped: null,
    no_mongodb_log: false,
    no_mongodb_state: false,
    no_mongodb_statistics: false,
    clear_mongodb: true,
    playback_speed: null,
    start_time: '2024-10-01T00:00',
    end_time: '2024-12-01T00:00',
  };

  messageReplayResponse$!: Observable<MessageReplayResponse>;

  constructor(
    private messageReplayService: MessageReplayService,
  ) { }

  startMessageReplay() {
    this.messageReplayResponse$ = this.messageReplayService.startMessageReplay(this.message_replay_request);
  }
}
