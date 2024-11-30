import { TestBed } from '@angular/core/testing';

import { MessageReplayService } from './message-replay.service';

describe('MessageReplayService', () => {
  let service: MessageReplayService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MessageReplayService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
