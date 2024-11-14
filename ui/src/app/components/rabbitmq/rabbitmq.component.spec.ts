import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RabbitmqComponent } from './rabbitmq.component';

describe('RabbitmqComponent', () => {
  let component: RabbitmqComponent;
  let fixture: ComponentFixture<RabbitmqComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RabbitmqComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RabbitmqComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
