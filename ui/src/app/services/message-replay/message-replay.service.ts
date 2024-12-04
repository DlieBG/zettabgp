import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { MessageReplayRequest, MessageReplayResponse } from '../../types/message-replay.type';

@Injectable({
  providedIn: 'root'
})
export class MessageReplayService {

  constructor(
    private httpClient: HttpClient,
  ) { }

  startMessageReplay(MessageReplayRequest: MessageReplayRequest): Observable<MessageReplayResponse> {
    return this.httpClient.post<MessageReplayResponse>('api/message-replay/', MessageReplayRequest);
  }

}
