import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeviceDetailsComponent } from './device-details.component';
import { RouterTestingModule } from '@angular/router/testing';

import { ApiModule } from '../api/api.module';

describe('DeviceDetailsComponent', () => {
  let component: DeviceDetailsComponent;
  let fixture: ComponentFixture<DeviceDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeviceDetailsComponent ],
      imports: [ 
        RouterTestingModule,
        ApiModule,
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeviceDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
