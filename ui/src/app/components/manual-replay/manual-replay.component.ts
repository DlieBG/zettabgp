import { Component } from '@angular/core';
import { MessageReplayResponse } from '../../types/message-replay.type';
import { Observable } from 'rxjs';
import { MessageReplayService } from '../../services/message-replay/message-replay.service';

@Component({
  selector: 'app-manual-replay',
  templateUrl: './manual-replay.component.html',
  styleUrl: './manual-replay.component.scss'
})
export class ManualReplayComponent {
  rabbitmq_direct = true;
  rabbitmq_grouped = null;
  mongodb_log = false;
  mongodb_state = false;
  mongodb_statistics = false;
  clear_mongodb = true;
  playback_speed = null;
  start_time = '2024-10-01T00:00';
  end_time = '2024-12-01T00:00';

  messageReplayResponse$!: Observable<MessageReplayResponse>;

  constructor(
    private messageReplayService: MessageReplayService,
  ) { }

  startMessageReplay() {
    this.messageReplayResponse$ = this.messageReplayService.startMessageReplay({
      no_rabbitmq_direct: !this.rabbitmq_direct,
      rabbitmq_grouped: this.rabbitmq_grouped,
      no_mongodb_log: !this.mongodb_log,
      no_mongodb_state: !this.mongodb_state,
      no_mongodb_statistics: !this.mongodb_statistics,
      clear_mongodb: this.clear_mongodb,
      playback_speed: this.playback_speed,
      start_time: this.start_time,
      end_time: this.end_time,
    });
  }
}
