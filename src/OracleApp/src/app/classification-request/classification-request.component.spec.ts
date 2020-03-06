import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassificationRequestComponent } from './classification-request.component';

describe('ClassificationRequestComponent', () => {
  let component: ClassificationRequestComponent;
  let fixture: ComponentFixture<ClassificationRequestComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ClassificationRequestComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ClassificationRequestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
