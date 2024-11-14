import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MrtScenarioComponent } from './mrt-scenario.component';

describe('MrtScenarioComponent', () => {
  let component: MrtScenarioComponent;
  let fixture: ComponentFixture<MrtScenarioComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MrtScenarioComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MrtScenarioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
