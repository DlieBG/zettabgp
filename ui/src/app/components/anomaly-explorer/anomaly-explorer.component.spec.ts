import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnomalyExplorerComponent } from './anomaly-explorer.component';

describe('AnomalyExplorerComponent', () => {
  let component: AnomalyExplorerComponent;
  let fixture: ComponentFixture<AnomalyExplorerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AnomalyExplorerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AnomalyExplorerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
