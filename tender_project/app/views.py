from django.shortcuts import render,HttpResponse, get_object_or_404,redirect
from. models import Proposal,Section
from .forms import ProposalForm, SectionForm,RegistrationForm
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def register(request):
    """
    View function for user registration.If the request method is POST, the function attempts to process the registration form.
    If the form is valid, a new user is created, logged in, and redirected to the login page.
    If the request method is GET, the registration form is initialized for rendering.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to your home or dashboard page
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    """
    View function for handling user login.
    If the request method is POST, it attempts to authenticate the user using the provided credentials.
    If authentication is successful, the user is logged in, and they are redirected to the 'home' view.
    If authentication fails or the request method is GET, it initializes an AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # Log in the user
                login(request, user)
                return redirect('proposal_list')  # Redirect to 'home' or any other view after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def proposal_list(request):
    """
    View function for displaying a list of proposals associated with the logged-in user.
    This view fetches a list of proposals filtered by the user's ID and renders them in 
    the 'index.html' template.
    """
    proposals = Proposal.objects.filter(user=request.user.id) # Access user ID
    return render(request, 'index.html', {'proposals': proposals})

@login_required
def add_proposal(request):
    """    
    View function for handling the addition of a new proposal.
    If the request method is POST, it validates the form data and creates a new proposal associated with the logged-in user.
    If the form is valid, the proposal is saved, and the user is redirected to the 'proposal_list' view.
    If the request method is GET, it initializes an empty ProposalForm.
    """

    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.user = request.user
            proposal.save()
            return redirect('proposal_list')  # Assuming you have a view named 'proposal_list'
    else:
        form = ProposalForm()

    return render(request, 'add_proposal.html', {'form': form})

@login_required
def add_section(request, proposal_id):
    """
    View function for handling the addition of a new section to a specific proposal.
    Fetches the specified proposal using the provided proposal_id.
    If the request method is POST, it validates the form data and creates a new section associated with the proposal.
    If the form is valid, the section is saved, and the user is redirected to the 'proposal_list' view.
    If the request method is GET, it initializes an empty SectionForm."""
    proposal = Proposal.objects.get(proposal_id=proposal_id)

    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.proposal = proposal
            section.save()
            return redirect('proposal_list')  # Redirect to 'proposal_list' without passing proposal_id
    else:
        form = SectionForm()

    return render(request, 'add_section.html', {'form': form, 'proposal': proposal,'proposal_id':proposal_id})


@login_required
def edit_section(request, proposal_id, section_id):
    """
    View function for editing an existing section within a proposal.
    Retrieves the specified section using the provided section_id.
    If the request method is POST, it validates the form data and updates the section.
    If the form is valid, the changes are saved, and the user is redirected to the 'proposal_list' view for the proposal.
    If the request method is GET, it initializes a SectionForm with the current section details.
    """
    section = get_object_or_404(Section, id=section_id)

    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('proposal_list', proposal_id=proposal_id)
    else:
        form = SectionForm(instance=section)

    return render(request, 'edit_section.html', {'form': form, 'proposal_id': proposal_id, 'section': section})

@login_required
def edit_proposal(request, proposal_id):
    """
    View function for editing an existing proposal.
    Retrieves the specified proposal using the provided proposal_id.
    If the request method is POST, it validates the form data and updates the proposal.
    If the form is valid, the changes are saved, and the user is redirected to the 'proposal_list' view.
    If the request method is GET, it initializes a ProposalForm with the current proposal details.

    """
    proposal = get_object_or_404(Proposal, proposal_id=proposal_id)

    if request.method == 'POST':
        form = ProposalForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            return redirect('proposal_list')
    else:
        form = ProposalForm(instance=proposal)

    return render(request, 'edit_proposal.html', {'form': form, 'proposal': proposal})
@login_required
def delete_section(request, proposal_id):
    """
    View function for deleting a proposal and its associated sections.
    Retrieves the specified proposal using the provided proposal_id and deletes it.
    """
    # Get the proposal
    proposal = get_object_or_404(Proposal, proposal_id=proposal_id)

    # Delete the section
    proposal.delete()

    # Redirect to the proposal detail view or any other appropriate view
    return redirect('proposal_list')




def generate_pdf(request, proposal_id):
    """
    View function for generating a PDF document from a proposal.
    Retrieves the specified proposal using the provided proposal_id.
    """
    # Get your proposal data
    proposal = get_object_or_404(Proposal, proposal_id=proposal_id)

    # Prepare the context for rendering the HTML template
    context = {'proposal': proposal}

    # Render the HTML template
    template_path = 'proposal_pdf.html'  # Update with your actual template path
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="proposal_{proposal_id}.pdf"'

    # Generate the PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisa_status.err, html))
    return response

def user_logout(request):
    """
    View function for handling user logout.
    Logs out the currently logged-in user and redirects to the 'home' page.
    """
    logout(request)
    return redirect('login')  # Redirect to your home or dashboard page


