import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConnectionHelperComponent } from './connection-helper.component';

describe('ConnectionHelperComponent', () => {
  let component: ConnectionHelperComponent;
  let fixture: ComponentFixture<ConnectionHelperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ConnectionHelperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConnectionHelperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
