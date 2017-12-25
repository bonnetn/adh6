import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeviceNewComponent } from './device-new.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ApiModule } from '../api/api.module';
import { RouterTestingModule } from '@angular/router/testing';

describe('DeviceNewComponent', () => {
  let component: DeviceNewComponent;
  let fixture: ComponentFixture<DeviceNewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeviceNewComponent ],
      imports: [ ReactiveFormsModule, ApiModule, RouterTestingModule ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeviceNewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
