import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MessageReplayComponent } from './message-replay.component';

describe('MessageReplayComponent', () => {
  let component: MessageReplayComponent;
  let fixture: ComponentFixture<MessageReplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MessageReplayComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MessageReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
