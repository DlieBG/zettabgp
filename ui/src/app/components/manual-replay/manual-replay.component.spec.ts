import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManualReplayComponent } from './manual-replay.component';

describe('ManualReplayComponent', () => {
  let component: ManualReplayComponent;
  let fixture: ComponentFixture<ManualReplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManualReplayComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManualReplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
