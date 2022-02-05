import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EntitiesListsComponent } from './entities-lists.component';

describe('EntitiesListsComponent', () => {
  let component: EntitiesListsComponent;
  let fixture: ComponentFixture<EntitiesListsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EntitiesListsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EntitiesListsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
