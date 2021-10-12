# Generated by Django 3.1.2 on 2021-05-20 10:59

import app_organizations.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import organizations.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(help_text='The name of the organization', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('slug', organizations.fields.SlugField(blank=True, editable=False, help_text='The name in all lowercase, suitable for URL identification', max_length=200, populate_from='name', unique=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='organizations/avatars')),
            ],
            options={
                'verbose_name': 'organization',
                'verbose_name_plural': 'organizations',
                'ordering': ['name'],
                'abstract': False,
                'proxy': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('authority', models.PositiveIntegerField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_organizations.apporganization')),
                ('permissions', models.ManyToManyField(blank=True, related_name='organization_group_set', related_query_name='organization_group', to='auth.Permission', verbose_name='permissions')),
            ],
            options={
                'verbose_name': 'organization group',
                'verbose_name_plural': 'organization groups',
                'unique_together': {('name', 'organization')},
            },
            managers=[
                ('objects', app_organizations.models.OrganizationGroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='AppOrganizationUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The organization groups this organization user belongs to. A organization user will get all permissions granted to each of their groups.', related_name='organization_user_set', related_query_name='organization_user', to='app_organizations.OrganizationGroup', verbose_name='organization groups')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_users', to='app_organizations.apporganization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_organizations_apporganizationuser', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this organization user.', related_name='organization_user_set', related_query_name='organization_user', to='auth.Permission', verbose_name='organization permissions')),
            ],
            options={
                'verbose_name': 'organization user',
                'verbose_name_plural': 'organization users',
                'ordering': ['organization', 'user'],
                'abstract': False,
                'proxy': False,
                'unique_together': {('user', 'organization')},
            },
        ),
        migrations.CreateModel(
            name='AppOrganizationOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='app_organizations.apporganization')),
                ('organization_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_organizations.apporganizationuser')),
            ],
            options={
                'verbose_name': 'organization owner',
                'verbose_name_plural': 'organization owners',
                'abstract': False,
                'proxy': False,
            },
        ),
        migrations.CreateModel(
            name='AppOrganizationInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('guid', models.UUIDField(editable=False)),
                ('invitee_identifier', models.CharField(help_text='The contact identifier for the invitee, email, phone number, social media handle, etc.', max_length=1000)),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_organizations_apporganizationinvitation_sent_invitations', to=settings.AUTH_USER_MODEL)),
                ('invitee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='app_organizations_apporganizationinvitation_invitations', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_invites', to='app_organizations.apporganization')),
            ],
            options={
                'verbose_name': 'organization invitation',
                'verbose_name_plural': 'organization invitations',
                'abstract': False,
                'proxy': False,
            },
        ),
        migrations.AddField(
            model_name='apporganization',
            name='users',
            field=models.ManyToManyField(related_name='app_organizations_apporganization', through='app_organizations.AppOrganizationUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
